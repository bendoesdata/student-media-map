<template>
  <div id="app">
    <div class="intro">
    <h1>Explore the {{ totalNumOutlets }} Student Media Outlets Across the U.S.</h1>
    <p>Use the map below to discover various student media outlets located at colleges and universities nationwide. Click on the markers to learn more about each outlet and visit their websites.</p>
    </div>
    <MapComponent />
    </div>
</template>

<script>
import MapComponent from './components/MapComponent.vue';
import Papa from 'papaparse';

export default {
  name: 'App',
  components: {
    MapComponent,
  },
  data() {
    return {
      totalNumOutlets: 0
    };
  },
  mounted() {
    // fp for local dev
      // let fp = 'https://bendoesdata.github.io/student-media-map/outlets.csv';
      // fp for prod dev
      let fp = '/student-media-map/outlets.csv';

    // load the csv file to get the total number of outlets
    fetch(fp)
      .then(response => response.text())
      .then(csvText => {
        // Parse the CSV data
        Papa.parse(csvText, {
          header: true,
          complete: (results) => {
            this.totalNumOutlets = results.data.length.toLocaleString();
          }
        });
      })
      .catch(error => {
        console.error("Error fetching or parsing CSV:", error);
      });
  }
};
</script>

<style>
/* Basic styles for the app container */
#app {
  margin: 0;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  padding: 0px;
  height: 100%;
  width: 100%;
  text-align: center;
  overflow: hidden; /* Prevent scrolling */
}

.intro {
  max-width: 750px;
  text-align: center;
  margin: 0 auto 20px;
}

h1 {
  font-size: 1.5rem
}
</style>