<template>
  <div id="app">
    <div class="intro">
    <h1>Explore Student Media Outlets Across the U.S.</h1>
    <p>Use the map below to discover various student media outlets located at colleges and universities nationwide. Click on the markers to learn more about each outlet and visit their websites.</p>
    </div>
    <MapComponent />
    </div>
</template>

<script>
import MapComponent from './components/MapComponent.vue';

export default {
  name: 'App',
  components: {
    MapComponent,
  },
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
</style>