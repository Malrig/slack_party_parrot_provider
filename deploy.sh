#!/bin/bash
# Define a small function for exiting the script with an error message
die() {
  printf '%s\n' "$1" >&2
  exit 1
}

# Exit if any command fails
set -e

# Set up local variables
commit_id=""
staging_deploy=false

while :; do
  case $1 in
    -c|--commit_id)       # Takes an option argument; ensure it has been specified.
      if [ "$2" ]; then
        commit_id=$2
        shift
      else
        die 'ERROR: "--commit_id" requires a non-empty option argument.'
      fi
      ;;
    --commit_id=?*)
      commit_id=${1#*=} # Delete everything up to "=" and assign the remainder.
      ;;
    --commit_id=)         # Handle the case of an empty --file=
      die 'ERROR: "--target_ip" requires a non-empty option argument.'
      ;;
    --)
      shift
      break
      ;;

    -s|--staging)
      echo "Deploy to the test directory"
      staging_deploy=true
      ;;

    -?*)
      printf 'WARN: Unknown option (ignored): %s\n' "$1" >&2
      ;;
    *)               # Default case: No more options, so break out of the loop.
      break
  esac

  shift
done

# The commit ID is required otherwise don't know what to deploy.
if [ -z "commit_id" ]; then
  die 'ERROR: you must provide a value for the commit ID using "--commit_id" or "-c".'
fi


ssh -p 22022 $SSH_LOGIN_USERNAME@georgeblackburn.co.uk << EOF
  pwd
  if [[ "$staging_deploy" = true ]]; then
    cd /var/WebApps/slack_party_parrot_provider_test/
  else
    cd /var/WebApps/slack_party_parrot_provider/
  fi
  pwd

  git fetch
  git checkout $commit_id
  source slack_party_parrot_provider_env/bin/activate
  pip install -r requirements.txt

  touch run.py
EOF