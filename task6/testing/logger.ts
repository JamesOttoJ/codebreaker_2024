import * as log from "https://deno.land/std/log/mod.ts";

await log.setup({
    handlers: {
        console: new log.ConsoleHandler("DEBUG", {
//            formatter: "{datetime} {levelName} {msg}"
            formatter: rec => JSON.stringify({t: rec.datetime, l: rec.levelName, m: rec.msg})
    }),
  },
  loggers: {
      default: {
          level: "INFO",
          handlers: ["console"],
    },
  },
});

export const logger = log;

