<template>
  <div id="app">
    <h1>Explore the {{ totalNumOutlets }} Student Newspapers Across the U.S.</h1>
    <div class="intro">
    <p>Use the map below to discover our continuously updated list of student newspapers at colleges and universities nationwide. Click on the markers to learn about each outlet and visit their websites.</p>
    <p>To add your student newspaper to the map, fill out this short form.</p>
    <p>To report an error within this map, please email Barbara Allen at bob@collegejournalism.org.</p> 
    </div>
    <br></br>
  <OutletSearchBar @college-selected="handleCollegeSelected" />
  <MapComponent :selectedCollege="selectedCollege" />
    </div>
</template>

<script>
import MapComponent from './components/MapComponent.vue';
import Papa from 'papaparse';
import OutletSearchBar from './components/OutletSearchBar.vue';

export default {
  name: 'App',
  components: {
    MapComponent,
    OutletSearchBar
  },
  data() {
    return {
      totalNumOutlets: 0,
      selectedCollege: ''
    };
  },
  methods: {
    handleCollegeSelected(college) {
      this.selectedCollege = college;
    }
  },
  mounted() {
    // fp for local dev
    let fp = 'https://bendoesdata.github.io/student-media-map/outlets.csv';
    // fp for prod dev
    // let fp = '/outlets.csv';

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

p {
  font-size: 1.2rem;
  line-height: 1.2;
  margin: 20px 0;
}

.intro {
  max-width: 580px;
  text-align: left;
  margin: 0 auto;
  margin-bottom: 20px;
  padding: 0px
}

h1 {
  font-size: 2rem;
  text-align: center;;
  margin-bottom: 20px
}

@media (max-width: 600px) {
.intro {
  padding: 8px
}

h1 {
  font-size: 1.6rem;
}
}
</style>