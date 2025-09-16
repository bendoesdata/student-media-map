<template>
  <div id="map-wrapper">
    <div id="sidebar">
      <p style="font-style: italic; font-size: 14px">Select a marker to learn more about each student media outlet.</p>
      <hr>
      <div v-if="selectedOutlet">
        <h3> {{ selectedOutlet['Name of Outlet'] }}</h3>
        <p><strong>Website:</strong> <a :href="selectedOutlet['URL of Outlet']" target="_blank">{{ selectedOutlet['URL of Outlet'] }}</a></p>
        <p><strong>Contact page:</strong> <a :href="selectedOutlet['Contact page']" target="_blank">{{ selectedOutlet['Contact page'] }}</a></p>
        <p><strong>Editor/Contact:</strong> {{ selectedOutlet['Editor/Contact'] }}</p>
        <p><strong>Title:</strong> {{ selectedOutlet['Title'] }}</p>
        <p><strong>Editor/General email:</strong> {{ selectedOutlet['Editor/General email'] }}</p>
        <p><strong>Adviser/Pro staff:</strong> {{ selectedOutlet['Adviser/Pro staff'] }}</p>
      </div>
    </div>
    <div id="map"></div>
  </div>
</template>

<script>
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import Papa from 'papaparse';

export default {
  name: 'MapComponent',
  props: {
    selectedCollege: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      selectedOutlet: null,
      outletsData: []
    };
  },
  mounted() {
    this.initMap();
    this.fetchDataAndAddMarkers();
  },
  watch: {
    selectedCollege(newCollege) {
      if (newCollege && this.outletsData.length) {
        // Find the first outlet with matching college name
        const outlet = this.outletsData.find(o => o['College/University'] === newCollege);
        if (outlet && !isNaN(parseFloat(outlet.LAT)) && !isNaN(parseFloat(outlet.LONG))) {
          this.map.setView([parseFloat(outlet.LAT), parseFloat(outlet.LONG)], 12, { animate: true });
          this.selectedOutlet = outlet;
        }
      }
    }
  },
  methods: {
    initMap() {
      // Initialize the map and set a default view
      this.map = L.map('map').setView([39.8283, -98.5795], 4);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        minZoom: 0,
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(this.map);
    },
    fetchDataAndAddMarkers() {
      // fp for local dev
      // let fp = 'https://bendoesdata.github.io/student-media-map/outlets.csv';
      // fp for prod dev
      let fp = '/student-media-map/outlets.csv';

      // Fetch the local CSV file
      fetch(fp)
        .then(response => response.text())
        .then(csvText => {
          // Parse the CSV data
          Papa.parse(csvText, {
            header: true,
            complete: (results) => {
              this.outletsData = results.data;
              this.addMarkers(results.data);
            }
          });
        })
        .catch(error => {
          console.error("Error fetching or parsing CSV:", error);
        });
    },
    addMarkers(data) {
      // Define a smaller icon for the markers
      const smallIcon = L.icon({
        iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
        iconSize: [20, 32], // default is [25, 41]
        iconAnchor: [10, 32], // default is [12, 41]
        popupAnchor: [1, -32], // default is [1, -34]
        shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
        shadowSize: [32, 32], // default is [41, 41]
        shadowAnchor: [10, 32] // default is [12, 41]
      });

      data.forEach(outlet => {
        // Ensure the data has LAT and LONG and they are valid numbers
        const lat = parseFloat(outlet.LAT);
        const long = parseFloat(outlet.LONG);

        if (!isNaN(lat) && !isNaN(long)) {
          // Create the marker with the smaller icon and add it to the map
          const marker = L.marker([lat, long], { icon: smallIcon }).addTo(this.map);

          // Create the popup content
          const popupContent = `
            <h3>${outlet['Name of Outlet']}</h3>
            <p>${outlet['College/University']}</p>
          `;

          // Bind the popup to the marker
          marker.bindPopup(popupContent);

          // Add click event to populate sidebar
          marker.on('click', () => {
            this.selectedOutlet = outlet;
          });
        }
      });
    }
  }
};
</script>

<style>
#map {
  height: 100vh; /* Make the map fill the entire screen height */
  width: 66%;
  margin: 0 10px;
  box-sizing: border-box;

}

#map-wrapper {
  display: flex;
}
#sidebar {
  width: 33%;
  padding: 20px;
  box-sizing: border-box;
  background-color: #f9f9f9;
  border: 2px solid #333;
  text-align: left;
}

@media (max-width: 768px) {
  #map-wrapper {
    flex-direction: column;
  }
  #sidebar {
    width: 100%;
    margin-bottom: 20px;
    text-align: left;
    padding: 10px;
  }
  #map {
    width: 100%;
    height: 70vh; /* Adjust height for smaller screens */
  }
}
</style>