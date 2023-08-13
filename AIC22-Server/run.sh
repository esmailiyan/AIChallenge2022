rm logs/server.log
rm logs/details.log
rm ../AIC22-Client-Python/log.txt
touch ../AIC22-Client-Python/log.txt
java -jar hideandseek-0.1.4.jar --first-team="../AIC22-Client-Python/dist/client" --second-team="../AIC22-Client-Python/dist/client" "map.yml" "map.json"
