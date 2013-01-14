# giraffe-collectd #

A simple [Giraffe](http://github.com/kenhub/giraffe) configuration generator for collectd metrics in Graphite (pushed via [chef-collectd](http://github.com/hectcastro/chef-collectd) or others).

## Usage ##

### Installation ###

* Save giraffe-collectd.py to a useful location
* Ensure giraffe-collectd.py configuration at top is correct for your environment
* Run giraffe-collectd.py (or better yet setup a crontab)
* Add the following line to your Giraffe index.html below the dashboards.js line:

    <script src="dashboards-collectd.js"></script>

* Comment out the `var dashboards` section of Giraffe dashboards.js

## Contributing ##

Please use standard Github issues/pull requests.

## License and Author ##
      
Author:: Brian Flad (<bflad417@gmail.com>)

Copyright:: 2013

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
