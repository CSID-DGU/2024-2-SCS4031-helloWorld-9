<script>
  import Router from 'svelte-spa-router';
  import routes from './routes';

  const API_KEY = import.meta.env.VITE_OPENAI_API_KEY;
</script>

<div class="sidebar">
  <h2>Menu</h2>
  <nav>
    <a href="#/pdfmanager">PDF 관리</a>
    <a href="#/chatbot">챗봇</a>
    <a href="#/graphview">그래프뷰</a>
  </nav>
</div>

<div class="main-content">
  <Router {routes} />
</div>

<style>
  body {
    font-family: Arial, sans-serif;
    margin: 0;
    background-color: #f0f2f5;
    color: #333;
    font-size: 30px;
  }

  .sidebar {
    width: 250px;
    background-color: #e07100;
    color: #fff;
    display: flex;
    flex-direction: column;
    padding: 20px;
    position: fixed;
    height: 100vh;
    top: 0;
    left: 0;
    border-radius: 0 15px 15px 0;
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  }

  .sidebar h2 {
    color: #fff;
    font-size:25px;
    margin-bottom: 20px;
    font-weight: 600;
    padding-bottom: 15px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  }

  .sidebar nav a {
    color: rgba(255, 255, 255, 0.9);
    padding: 12px 15px;
    text-decoration: none;
    font-size:25px;
    display: block;
    border-radius: 10px;
    margin-bottom: 5px;
    transition: all 0.3s ease;
  }

  .sidebar nav a:hover {
    background-color: rgba(255, 255, 255, 0.1);
    color: #fff;
    transform: translateX(5px);
  }

  .main-content {
    margin-left: 270px;
    padding: 20px;
    overflow-y: auto;
    flex: 1;
    min-height: calc(100vh - 40px);
  }
</style>