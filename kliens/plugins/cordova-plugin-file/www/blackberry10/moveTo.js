/*
 *
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 *
*/

/*
 * moveTo
 *
 * IN:
 *  args
 *   0 - URL of entry to move
 *   1 - URL of the directory into which to move the entry
 *   2 - the new name of the entry, defaults to the current name
 * OUT:
 *  success - entry for the copied file or directory
 *  fail - FileError
 */

var copy = cordova.require('cordova-plugin-file.copyToProxy'); // eslint-disable-line no-undef

module.exports = function (success, fail, args) {
    copy(success, fail, args, true);
};
