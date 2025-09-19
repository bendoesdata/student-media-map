<template>
  <div class="search-bar">
    <input
      type="text"
      v-model="searchQuery"
      @input="onInput"
      placeholder="Search College/University..."
      autocomplete="off"
    />
    <ul v-if="filteredColleges.length && searchQuery">
      <li v-for="college in filteredColleges" :key="college" @click="selectCollege(college)">
        {{ college }}
      </li>
    </ul>
  </div>
</template>

<script>
import Papa from 'papaparse';

export default {
  name: 'OutletSearchBar',
  data() {
    return {
      colleges: [],
      searchQuery: '',
      filteredColleges: []
    };
  },
  mounted() {
    this.loadColleges();
  },
  methods: {
    loadColleges() {

        // fp for local dev
      let fp = 'https://bendoesdata.github.io/student-media-map/outlets.csv';
      // fp for prod dev
    //   let fp = '/student-media-map/outlets.csv';

      fetch(fp)
        .then(response => response.text())
        .then(csvText => {
          Papa.parse(csvText, {
            header: true,
            complete: (results) => {
              const allColleges = results.data.map(row => row['College/University']).filter(Boolean);
              this.colleges = [...new Set(allColleges)].sort();
            }
          });
        })
        .catch(error => {
          console.error('Error loading CSV:', error);
        });
    },
    onInput() {
      const query = this.searchQuery.toLowerCase();
      this.filteredColleges = this.colleges.filter(college =>
        college.toLowerCase().includes(query)
      );
    },
    selectCollege(college) {
      this.searchQuery = college;
      this.filteredColleges = [];
      // Optionally emit an event to parent
      this.$emit('college-selected', college);
    }
  }
};
</script>

<style scoped>
.search-bar {
  position: relative;
  width: 100%;
  max-width: 400px;
  margin: 20px auto;
  z-index: 999;
}
input {
  width: 100%;
  padding: 8px;
  font-size: 16px;
}
ul {
  position: absolute;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #ccc;
  max-height: 200px;
  overflow-y: auto;
  margin: 0;
  padding: 0;
  list-style: none;
  z-index: 10;
}
li {
  padding: 8px;
  cursor: pointer;
}
li:hover {
  background: #f0f0f0;
}
</style>
