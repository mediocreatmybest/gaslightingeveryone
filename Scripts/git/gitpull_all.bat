for /D %%G in ("*") do (echo %%G) && (cd %%G) && (git pull) && (cd ..)
pause