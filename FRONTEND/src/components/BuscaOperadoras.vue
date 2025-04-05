<template>
  <div class="page">
    <div class="top-bar">
      <h1>Buscar Operadoras da ANS</h1>
      <div class="search-area">
        <input v-model="termo" placeholder="Digite o nome da operadora" />
        <button @click="buscar">Buscar</button>
      </div>
    </div>

    <div class="conteudo">
      <ul v-if="resultados.length">
        <li v-for="(op, index) in resultados" :key="index">
          <strong>{{ op.nome_fantasia || 'Sem nome fantasia' }}</strong><br />
          Razão social: {{ op.razao_social || 'N/A' }}<br />
          Município: {{ op.municipio || 'N/A' }} ({{ op.uf || 'N/A' }})
        </li>
      </ul>
      <p v-else>Nenhum resultado ainda.</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const termo = ref('')
const resultados = ref([])

const buscar = async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:5000/busca?q=${termo.value}`)
    // Se o backend retornar JSON já parseado, atribuímos diretamente:
    resultados.value = res.data
  } catch (err) {
    console.error("Erro na API:", err)
  }
}
</script>

<style scoped>
body {
  margin: 0;
  background-color: #121212;
  color: #fff;
  font-family: sans-serif;
}

.page {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 1rem;
}

.top-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem 1rem;
  background-color: #121212;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.6);
  z-index: 10;
}

.top-bar h1 {
  text-align: center;
  margin-bottom: 1rem;
}

.search-area {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.search-area input {
  flex: 1;
  padding: 1rem;
  border-radius: 12px;
  border: none;
  font-size: 1rem;
  min-width: 250px;
}

.search-area button {
  padding: 1rem 1.5rem;
  border-radius: 12px;
  background-color: #007BFF;
  border: none;
  color: white;
  font-size: 1rem;
  cursor: pointer;
}

.search-area button:hover {
  background-color: #005fcc;
}

.conteudo {
  padding-top: 180px;       
  max-width: 800px;
  margin: 0 auto;
  padding-left: 1rem;
  padding-right: 1rem;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

li {
  background-color: #1e1e1e;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  margin-bottom: 1rem;
  text-align: left;
  box-shadow: 0 1px 4px rgba(255, 255, 255, 0.05);
  margin-left: 300px;
  width: 100%;               
  max-width: 100%;           
  word-wrap: break-word;     
}
</style>
