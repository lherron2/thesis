#!/usr/bin/env bash
set -euo pipefail

HOST=10.0.0.209
KEY=/tmp/gk-ec2-access.pem

ssh -o StrictHostKeyChecking=no -i "$KEY" ec2-user@"$HOST" \
  'mkdir -p /home/ec2-user/RNAnneal /home/ec2-user/rnanneal_probe_sources /home/ec2-user/RNAnneal/containers/enroot'

tar -C /home/ec2-user/RNAnneal -cf - bin src ff \
  | ssh -o StrictHostKeyChecking=no -i "$KEY" ec2-user@"$HOST" 'tar -C /home/ec2-user/RNAnneal -xf -'

rm -rf /tmp/rnanneal_probe_sources_export
mkdir -p /tmp/rnanneal_probe_sources_export
while IFS= read -r sim; do
  repdir="$(basename "$(dirname "$sim")")"
  mkdir -p "/tmp/rnanneal_probe_sources_export/$repdir"
  cp "$sim" "/tmp/rnanneal_probe_sources_export/$repdir/simulator.h5"
  cp "$(dirname "$sim")/seed.h5" "/tmp/rnanneal_probe_sources_export/$repdir/seed.h5"
done < <(
  find /home/ec2-user/rnanneal_runs/gcauggcgaugc_md50ns_20260331/workdirs/0000_gcauggcgaugc/data/rosetta1/mount \
    -type f -name simulator.h5 | sort -V | head -n 16
)

tar -C /tmp/rnanneal_probe_sources_export -cf - . \
  | ssh -o StrictHostKeyChecking=no -i "$KEY" ec2-user@"$HOST" 'tar -C /home/ec2-user/rnanneal_probe_sources -xf -'

scp -q -o StrictHostKeyChecking=no -i "$KEY" \
  /home/ec2-user/RNAnneal/containers/enroot/rnanneal_py_cuda124.sqsh \
  ec2-user@"$HOST":/home/ec2-user/RNAnneal/containers/enroot/

ssh -o StrictHostKeyChecking=no -i "$KEY" ec2-user@"$HOST" \
  'du -sh /home/ec2-user/RNAnneal /home/ec2-user/rnanneal_probe_sources /home/ec2-user/RNAnneal/containers/enroot/rnanneal_py_cuda124.sqsh'
