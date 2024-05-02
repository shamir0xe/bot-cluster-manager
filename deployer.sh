#!/bin/bash
echo 'Deploying bot-manager procedure'

repository='https://github.com/shamir0xe/bot-cluster-manager.git'
app_dir=$(pwd)
output_dir=$app_dir/output
release_dir=$output_dir/releases
release=$(date +"%Y%m%d-%H%M%S")
new_release_dir=$release_dir/$release

echo 'Cloning repository'
[ -d "$release_dir" ] || mkdir -p "$release_dir"
git clone --depth 1 $repository "$new_release_dir" --recursive

echo 'Linking/Copying Environments'
rm -rf "$new_release_dir"/configs/env.json || true
cp "$app_dir"/configs/env.json "$new_release_dir"/configs/env.json
# ln -nfs "$app_dir"/configs/env.json "$new_release_dir"/configs/env.json

# echo 'Linking Assets'
# rm -rf "$new_release_dir"/assets
# ln -nfs "$app_dir"/assets "$new_release_dir"/assets

echo 'Unlinking previous release'
unlink "$output_dir"/current

echo 'Linking current release'
ln -nfs "$new_release_dir" "$output_dir"/current

echo 'Remove the previous image'
cd "$new_release_dir" || exit
docker image rm bot-manager --force || true

echo 'Creating the new image'
docker build -t bot-manager .

