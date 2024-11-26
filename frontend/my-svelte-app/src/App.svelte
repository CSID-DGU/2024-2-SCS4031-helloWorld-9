<script>
  import Router from 'svelte-spa-router';
  import routes from './routes';

  const API_KEY = import.meta.env.VITE_OPENAI_API_KEY;
</script>

<div class="sidebar">
  <h2>UI Components</h2>
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
  /* 전체 레이아웃 */
  body {
    font-family: Arial, sans-serif;
    margin: 0;
    background-color: #f4f5f7;
    color: #333;
    font-size: 18px;
  }

  /* 사이드바 스타일 */
  .sidebar {
    width: 250px;
    background-color: #343a40;
    color: #fff;
    display: flex;
    flex-direction: column;
    padding: 20px;
    position: fixed;
    height: 100vh;
    top: 0;
    left: 0;
    border-radius: 0 15px 15px 0;
  }

  .sidebar h2 {
    color: #fff;
    font-size: 20px;
    margin-bottom: 20px;
  }

  .sidebar nav a {
    color: #b8c2cc;
    padding: 10px 0;
    text-decoration: none;
    font-size: 18px;
    display: block;
  }

  .sidebar nav a:hover {
    color: #fff;
  }

  /* 메인 컨텐츠 */
  .main-content {
    margin-left: 270px;
    padding: 20px;
    overflow-y: auto;
    flex: 1;
  }
</style>