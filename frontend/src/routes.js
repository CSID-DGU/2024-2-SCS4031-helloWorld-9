import PdfManager from "./routes/Pdfmanager.svelte";
import Chatbot from "./routes/Chatbot.svelte";
import GraphView from "./routes/Graphview.svelte";

export default {
  "/pdfmanager": PdfManager,
  "/chatbot": Chatbot,
  "/graphview": GraphView,
};
