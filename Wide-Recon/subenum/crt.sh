#!/bin/bash

crtsh() {
    query=$(cat <<-END
        SELECT
            ci.NAME_VALUE
        FROM
            certificate_and_identities ci
        WHERE
            plainto_tsquery('certwatch', '$1') @@ identities(ci.CERTIFICATE)
END
    )

    echo "$query" | psql -t -h crt.sh -p 5432 -U guest certwatch | sed 's/ //g' | egrep ".*\.$1" | sed 's/\*\.//g' | tr '[:upper:]' '[:lower:]' | sort -u
}

crtsh "$@"