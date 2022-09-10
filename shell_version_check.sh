if curl "https://storage.googleapis.com/minecraft-server-config/version.txt" | grep -q "java"; then
    printf "Investigating Issue"
else
    printf "Fully Operational"
fi