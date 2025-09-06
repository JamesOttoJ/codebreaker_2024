console.debug = () => {} // stop debug logging for main app

import http from 'node:http';
// @deno-types="npm:@types/express"
import express from 'npm:express';
// @deno-types="npm:@types/body-parser"
import bodyParser from 'npm:body-parser';

import { connectToDatabase, closeDatabaseConnection, aggregateLocationEvents } from './mongodb.ts';
import { logger } from './logger.ts';
import { registerRoutes } from './routes.ts';

const app = express();
const port = Deno.env.get('PORT') || 3000;
const maintenanceInterval = parseInt(Deno.env.get('MAINTENANCE_INTERVAL') || '300000', 10); // default to 5 minutes
const uri = Deno.env.get('MONGODB_URI') || 'mongodb://localhost:27017';
const db = Deno.env.get('MONGODB_DB') || 'test';

app.use(bodyParser.json());
app.use(bodyParser.raw({ type: 'application/msgpack' }));

registerRoutes(app);

let server: http.Server;

connectToDatabase(uri, db).then(() => {
  server = app.listen(port, () => {
    logger.info(`Server is running on port ${port}`);
  });
  setInterval(async () => {
    try {
      await aggregateLocationEvents();
      logger.info('Maintenance task completed');
    } catch (err) {
      logger.error('Failed to run maintenance task', err);
    }
  }, maintenanceInterval);
}).catch(async (err) => {
  logger.error('Failed to connect to the database', err);
  await closeDatabaseConnection();
  Deno.exit(1);
});

const gracefulShutdown = async () => {
  logger.info('Received shutdown signal, closing server...');
  if (server) {
    server.close(async (err) => {
      if (err) {
        logger.error('Error closing server:', err);
        Deno.exit(1);
      }
      logger.info('Server closed');
      await closeDatabaseConnection();
      Deno.exit(0);
    });
  } else {
    await closeDatabaseConnection();
    Deno.exit(0);
  }
};

const handleSignal = async () => {
  logger.debug("handling signal, calling gracefulShutdown!")
  await gracefulShutdown();
  Deno.exit(0);
};

Deno.addSignalListener("SIGTERM", handleSignal);
Deno.addSignalListener("SIGINT", handleSignal);

