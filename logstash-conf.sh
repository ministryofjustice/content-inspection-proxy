#!/bin/bash
cat <<EOT

  input {
    file {
      path => "/cip/cip/cip.log"
      type => "cip"
      add_field => [ "project",   "$PROJECT" ]
      add_field => [ "appserver", "rails" ]
      add_field => [ "version",   "$APPVERSION" ]
      add_field => [ "env",       "$ENV" ]
    }
  }
  output {
    redis { host => "$LOGSTASH_SERVER" data_type => "list" key => "logstash" }
  }

EOT

