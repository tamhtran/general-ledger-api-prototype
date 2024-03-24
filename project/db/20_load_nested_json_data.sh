
# Load regions.json data into the regions and countries tables
echo "Loading nested json - regions and country data ..."
jq -c '.regions[]' /tmp/data/regions.json | while read region; do
    region_id=$(echo $region | jq '.id')
    region_name=$(echo $region | jq -r '.name')
    psql -U postgres -d web_dev -c "INSERT INTO regions (region_id, name) VALUES ($region_id, '$region_name')"

    echo $region | jq -c '.countries[]' | while read country; do
        country_id=$(echo $country | jq '.id')
        country_name=$(echo $country | jq -r '.name')
        psql -U postgres -d web_dev -c "INSERT INTO countries (country_id, name, region_id) VALUES ($country_id, '$country_name', $region_id)"
    done
done

echo "Loading nested json - regions and country data"
