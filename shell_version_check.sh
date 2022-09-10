if curl "https://storage.googleapis.com/minecraft-server-config/version.txt" | grep -q "java"; then
    cd /home/kensim28/spigot/
    java -DIReallyKnowWhatIAmDoingISwear -Xmx5096M -Xms5096M -jar /home/kensim28/spigot/spigot-1.19.2.jar nogui
else
    cd /home/kensim28/bedrock/
    /home/kensim28/bedrock/bedrock_server
fi