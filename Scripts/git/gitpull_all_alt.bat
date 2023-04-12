@echo off

REM # Check each folder in current working directory
for /D %%G in (*) do (
  REM # Check if the directory has git files (.git) what is the better alternative without calling git?)
  if exist "%%G\.git" (
    REM # echo folder name to make it easier to see folders that fail updates (stashed files etc)
    echo #########################################
    echo Updating git repository in %%G
    echo #########################################
    REM  # Run git command in folder
    pushd "%%G" && git pull && popd
  ) else (
    REM # skipping dir if it doesn't have .git files
    echo %%G is not a git repository, skipping...
  )
)

pause
