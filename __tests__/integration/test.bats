##
# Install the mkdocs-terraform-monorepo-plugin locally on test run.
#
pip install -e . --quiet >&2

##
# These are helper variables and functions written in Bash. It's like writing in your Terminal!
# Feel free to optimize these, or even run them in your own Terminal.
#

rootDir=$(pwd)
fixturesDir=${rootDir}/__tests__/integration/fixtures

debugger() {
  echo "--- STATUS ---"
  if [ $status -eq 0 ]
  then
    echo "Successful Status Code ($status)"
  else
    echo "Failed Status Code ($status)"
  fi
  echo "--- OUTPUT ---"
  echo $output
  echo "--------------"
}

assertFileExists() {
  run cat $1
  [ "$status" -eq 0 ]
}

assertSuccessMkdocs() {
  run mkdocs $@
  debugger
  assertFileExists site/index.html
  [ "$status" -eq 0 ]
}

assertFailedMkdocs() {
  run mkdocs $@
  debugger
  [ "$status" -ne 0 ]
}

##
# These are special lifecycle methods for Bats (Bash automated testing).
# setup() is ran before every test, teardown() is ran after every test.
#

teardown() {
  rm -rf ${fixturesDir}/**/*/site
}

##
# Test suites.
#

@test "builds a mkdocs site with minimal configuration" {
  cd ${fixturesDir}/ok-vanilla
  assertSuccessMkdocs build
  assertFileExists site/index.html
}



@test "builds a mkdocs site with single !tf_modules_root" {
  cd ${fixturesDir}/ok
  assertSuccessMkdocs build
  assertFileExists site/index.html
  assertFileExists site/project-a/b/index.html
  [[ "$output" == *"This contains a sentence which only exists in the ok/project-a/b fixture."* ]]
}


@test "builds a mkdocs site with mkdocs-monorepo-plugin" {
 cd ${fixturesDir}/ok-mkdocs-monorepo-plugin
 assertSuccessMkdocs build
 assertFileExists site/index.html
 assertFileExists site/test/index.html
 [[ "$output" == *"This contains a sentence which only exists in the ok-monorepo-plugin/project-a fixture."* ]]
 assertFileExists site/project-b/c/index.html
 [[ "$output" == *"This contains a sentence which only exists in the ok-monorepo-plugin/project-b fixture."* ]]
}


@test "builds a mkdocs site with a nested mkdocs-monorepo-plugin" {
 cd ${fixturesDir}/ok-mkdocs-monorepo-plugin-nested
 assertSuccessMkdocs build
 assertFileExists site/index.html
 assertFileExists site/test/index.html
 [[ "$output" == *"This contains a sentence which only exists in the ok-monorepo-plugin/project-a fixture."* ]]
 assertFileExists site/test/project-b/c/index.html
 [[ "$output" == *"This contains a sentence which only exists in the ok-monorepo-plugin/project-b fixture."* ]]
}


@test "fails if !tf_modules_root path does not exist" {
 cd ${fixturesDir}/error-include-path-not-found
 assertFailedMkdocs build
 [[ "$output" == *"[mkdocs-terraform-monorepo] The path ${fixturesDir}/project-a is not valid. Please update your 'nav' with a valid path (relative to the mkdocs.yml file)"* ]]
}

@test "fails if monorepo plugin before terraform-monorepo plugin config" {
 cd ${fixturesDir}/error-plugin-order-monorepo
 assertFailedMkdocs build
 [[ "$output" == *"[mkdocs-terraform-monorepo] terraform-monorepo should be defined after the monorepo plugin in your mkdocs.yml file"* ]]
}
