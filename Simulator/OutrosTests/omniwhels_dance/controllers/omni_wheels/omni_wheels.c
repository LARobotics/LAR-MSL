/*
 * Copyright 1996-2022 Cyberbotics Ltd.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/*
 * Description: Demo of a three-omni-wheels robot
 * Thanks to Mehdi Ghanavati, Shahid Chamran University
 */

#include <stdio.h>
#include <webots/motor.h>
#include <webots/robot.h>

static WbDeviceTag wheels[3];

static double cmd[5][3] = {
  {-2, 1, 1}, {0, 1, -1}, {2, -1, -1}, {0, -1, 1}, {2, 2, 2},
};

static double SPEED_FACTOR = 4.0;

int main() {
  int i;

  // initialize Webots
  wb_robot_init();

  for (i = 0; i < 3; i++) {
    char name[64];
    sprintf(name, "wheel%d", i + 1);
    wheels[i] = wb_robot_get_device(name);
    wb_motor_set_position(wheels[i], INFINITY);
  }

  while (1) {
    for (i = 0; i < 5; i++) {
        wb_motor_set_velocity(wheels[0], cmd[i][0] * SPEED_FACTOR);
        wb_motor_set_velocity(wheels[1], cmd[i][1] * SPEED_FACTOR);
        wb_motor_set_velocity(wheels[2], cmd[i][2] * SPEED_FACTOR);

      //for (k = 0; k < 100; k++)
        wb_robot_step(100);
    }
  }

  return 0;
}
