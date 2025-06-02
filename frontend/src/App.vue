<script setup>

</script>

<template>
  <div class="container">
    <h1> Scraped Apple Products 💻 </h1>

    <input
      v-model="search"
      placeholder="Search products..."
      class="search"
    />

    <div v-if="loading">Loading products...</div>

    <div v-else>
      <div
        v-for="product in filteredProducts"
        :key="product.id"
        class="product"
      >
        <h3>{{ product.name }}</h3>
        <p>{{ product.price }}</p>
        <a :href="product.link" target="_blank">View</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const products = ref([])
const loading = ref(true)
const search = ref("")

onMounted(async () => {
  try {
    // const response = await fetch("http://127.0.0.1:8000/products"); 
    const response = await fetch("/api/products");

    products.value = await response.json(); 
  } catch (err) {
    console.error("Failed to load products:", err)
  } finally {
    loading.value = false
  }
})

const filteredProducts = computed(() => {
  return products.value.filter((p) =>
    p.name?.toLowerCase().includes(search.value.toLowerCase())
  )
})
</script>

<style scoped>
.container {
  max-width: 700px;
  margin: 2rem auto;
  padding: 1rem;
  font-family: sans-serif;
}

.container h3{
  color: black;
}

.container p{
  color: black;
}

.search {
  width: 100%;
  padding: 8px;
  margin-bottom: 20px;
  font-size: 16px;
}

.product {
  border: 1px solid #ccc;
  padding: 12px;
  margin-bottom: 12px;
  border-radius: 6px;
  background: #f9f9f9;
}
</style>

