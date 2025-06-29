<script setup></script>

<template>
  <div class="container">
    <h1>Scraped Apple Products 💻</h1>

    <input
      v-model="search"
      placeholder="Upiši proizvod i pritisni Enter..."
      class="search"
      @keyup.enter="handleSearch"
    />

    <div v-if="loading">Učitavam...</div>
    <div v-if="statusMsg && !loading">{{ statusMsg }}</div>

    <div v-if="!loading && products.length > 0">
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
import { ref, computed } from "vue";

const products = ref([]);
const loading = ref(false);
const search = ref("");
const statusMsg = ref("");

const handleSearch = async () => {
  const keyword = search.value.trim();
  if (!keyword) return;

  loading.value = true;
  statusMsg.value = "Pokrećem scraper za: " + keyword;

  try {
    const res = await fetch(`/api/scraper?keyword=${keyword}`, {
      method: "POST",
    });
    const data = await res.json();
    console.log("Scraper pokrenut:", data.message);

    setTimeout(async () => {
      await loadProducts(keyword);
    }, 5000);
  } catch (err) {
    console.error("Greška:", err);
    statusMsg.value = "Došlo je do greške.";
    loading.value = false;
  }
  cd;
};

const loadProducts = async (category) => {
  try {
    const url = `/api/products?category=${category}`;
    const res = await fetch(url);
    const data = await res.json();
    products.value = data;
    statusMsg.value = `Nađeno ${data.length} proizvoda za "${category}".`;
  } catch (err) {
    console.error("Greška kod dohvaćanja proizvoda:", err);
    statusMsg.value = "Greška kod dohvaćanja proizvoda.";
  } finally {
    loading.value = false;
  }
};

const filteredProducts = computed(() => {
  const keyword = search.value.toLowerCase();
  return products.value.filter((p) => p.name?.toLowerCase().includes(keyword));
});
</script>

<style scoped>
.container {
  max-width: 700px;
  margin: 2rem auto;
  padding: 1rem;
  font-family: sans-serif;
}

.container h3,
.container p {
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
