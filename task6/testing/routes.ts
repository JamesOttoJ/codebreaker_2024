import { assert } from "jsr:@std/assert";
// @deno-types="npm:@types/express"
import { Application, Request, Response } from 'npm:express';
import { MongoClient } from 'npm:mongodb';
// @deno-types="npm:@types/msgpack-lite"
import msgpack from 'npm:msgpack-lite';
import { insertLocationEvent, LocationEvent } from "./mongodb.ts";

function unbias(i: number, f: number, a: number) {
  if ( 0 <= i && i <= a-1 ) { // originally positive
      i = i + 1
      return i - f
  } else if (a <= i && i <= 2*a) { // original negative (or zero)
      i = i - a
      let x = i - f
      if (x != 0) { // prefer 0 to -0
          x = -x
      }
      return x
  } else {
      console.log("Failed unbias")
      assert(false) // i not in [0, 2a]
  }
}

export function validateLocationEvent(req: Request): LocationEvent {
  const buffer = req.body
  console.log(buffer)
  // fast checks
  console.log("Checking buffer")
  assert(buffer[0] == 0x84) // must be object with 4 keys (v, t, d, m)
  assert(buffer[1] == 0xA1 && buffer[2] == 0x76) // first key is 'v'
  assert(buffer[3] == 0xA8 && buffer[4] == 0x4e) // vids are 8 character strings starting with N

  // slower msgpack decode and other validation

  const msg = msgpack.decode(buffer); // throws on bad decode

  let vid: string = msg.v // already checked above
  console.log("Checking vid")
  assert(vid) // fail fast
  let timestamp: number = msg.t // too old/new checked on event insert
  console.log("Checking timestamp")
  assert(timestamp) // fail fast

  // translate & check coordinates from msg.d (bias-packed degrees) and msg.m (bit-packed milliseconds)
  // convert to D.DDDDDD accuracy at least 0.000017 or approx 2 meters
  let lat_ms = (msg.m >> 16) & 0xFFFF
  let lon_ms = msg.m & 0xFFFF
  let lat_s = lat_ms / 1000
  let lon_s = lon_ms / 1000
  let lat_df = lat_s / 60
  let lon_df = lon_s / 60
  let lat_di = Math.trunc(msg.d / 361)
  let lon_di = (msg.d % 361)
  console.log("lat_di: " + lat_di + " | " + "lat_df: " + lat_df)
  console.log("lon_di: " + lon_di + " | " + "lon_df: " + lon_df)
  let lat: number = unbias(lat_di, lat_df, 90)
  let lon: number = unbias(lon_di, lon_df, 180)
  console.log("Checking lat and lon")
  assert(-90 <= lat && lat <= 90) // latitude range check.  range is [-90, 90]
  assert(-180 <= lon && lon <= 180) // longitude range check. range is [-180, 180]
  assert(!(lat == 0 && lon == 0)) // avoid bogus coordinates (null island)

  const event: LocationEvent = {
      vid: vid,
      timestamp: timestamp,
      point: {
          type: "Point",
          coordinates: [lon, lat] // GeoJSON Point expects longitude first
      }
  }

  return event
}

export function registerRoutes(app: Application) {
    app.post("/event/insert", async (req: Request, res: Response) => {
        try {
            const event = validateLocationEvent(req)
            await insertLocationEvent(event);
            res.status(200).send("Event inserted successfully");
        } catch (error) {
            res.status(500).send("Error inserting event: " + error);
        }
    });

    app.post("/event/test", async (req: Request, res: Response) => {
        try {
            const event: LocationEvent = {
                vid: "N-00-000",
                timestamp: (new Date()).getTime(),
                point: {
                    type: "Point",
                    coordinates: [0, 0] // visiting null island
                }
            };
            await insertLocationEvent(event);
            res.status(200).send("Event inserted successfully");
        } catch (error) {
            res.status(500).send("Error inserting event: " + error);
        }
    });

}
