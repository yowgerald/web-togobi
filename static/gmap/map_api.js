function initMap() {
    const input = document.getElementById("id_location");
    const options = {
      componentRestrictions: { country: "ph" },
      fields: ["address_components", "geometry", "icon", "name"],
      strictBounds: false,
    };
    const autocomplete = new google.maps.places.Autocomplete(input, options);
}