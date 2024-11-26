<script>
    import { onMount } from "svelte";
    import * as d3 from "d3";
  
    // 더미 데이터 (FAISS 결과에 해당)
    let graphData = {
      nodes: [
        { id: "보험" },
        { id: "보상" },
        { id: "가입" },
        { id: "이자" },
        { id: "청구" },
        { id: "리스크" },
        { id: "보장" },
        { id: "계약" },
      ],
      links: [
        { source: "보험", target: "보상", value: 0.8 },
        { source: "보험", target: "가입", value: 0.7 },
        { source: "보상", target: "이자", value: 0.6 },
        { source: "청구", target: "리스크", value: 0.9 },
        { source: "계약", target: "보험", value: 0.75 },
      ]
    };
  
    let svg, graphContainer;
  
    onMount(() => {
      const width = 2000;
      const height = 2000;
  
      // SVG 요소 및 컨테이너 설정
      svg = d3.select("#graph")
        .attr("width", width)
        .attr("height", height)
        .style("cursor", "move");
  
      graphContainer = svg.node().parentNode;  // svg 부모 컨테이너를 가져옴
  
      // 시뮬레이션 설정
      const simulation = d3.forceSimulation(graphData.nodes)
        .force("link", d3.forceLink(graphData.links).id(d => d.id).distance(200))
        .force("charge", d3.forceManyBody().strength(-500))
        .force("center", d3.forceCenter(width / 2, height / 2));
  
      // 링크 생성
      const link = svg.selectAll(".link")
        .data(graphData.links)
        .enter().append("line")
        .attr("class", "link")
        .attr("stroke", "#999")
        .attr("stroke-opacity", 0.6)
        .attr("stroke-width", d => Math.sqrt(d.value));
  
      // 노드 생성
      const node = svg.selectAll(".node")
        .data(graphData.nodes)
        .enter().append("circle")
        .attr("class", "node")
        .attr("r", 10)  // 노드 크기 축소
        .attr("fill", "skyblue")
        .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended));
  
      // 노드 이름 추가
      svg.selectAll(".node-label")
        .data(graphData.nodes)
        .enter().append("text")
        .attr("class", "node-label")
        .attr("x", 0)
        .attr("y", 20)  // 노드 밑에 텍스트 위치 조정
        .attr("text-anchor", "middle")
        .style("font-size", "10px")  // 텍스트 크기 축소
        .text(d => d.id);
  
      // 시뮬레이션 업데이트
      simulation.on("tick", () => {
        link.attr("x1", d => d.source.x)
          .attr("y1", d => d.source.y)
          .attr("x2", d => d.target.x)
          .attr("y2", d => d.target.y);
  
        node.attr("cx", d => d.x)
          .attr("cy", d => d.y);
  
        svg.selectAll(".node-label")
          .attr("x", d => d.x)
          .attr("y", d => d.y + 20); // 노드 아래 텍스트 위치 업데이트
      });
  
      // 드래그 시작
      function dragstarted(event) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        event.subject.fx = event.subject.x;
        event.subject.fy = event.subject.y;
      }
  
      // 드래그 중
      function dragged(event) {
        event.subject.fx = event.x;
        event.subject.fy = event.y;
      }
  
      // 드래그 종료
      function dragended(event) {
        if (!event.active) simulation.alphaTarget(0);
        event.subject.fx = null;
        event.subject.fy = null;
      }
  
      // 그래프 화면 드래그 기능
      let isDragging = false;
      let startX, startY;
  
      //마우스 이벤트로 화면 드래그 구현
      d3.select(graphContainer)
        .on("mousedown", (event) => {
          isDragging = true;
          startX = event.clientX;
          startY = event.clientY;
        })
        .on("mousemove", (event) => {
          if (isDragging) {
            const dx = event.clientX - startX;
            const dy = event.clientY - startY;
            startX = event.clientX;
            startY = event.clientY;
            const currentTransform = svg.attr("transform") || "translate(0,0)";
            const [currentX, currentY] = currentTransform.replace("translate(", "").replace(")", "").split(",").map(Number);
            svg.attr("transform", `translate(${currentX + dx},${currentY + dy})`);
          }
        })
        .on("mouseup", () => {
          isDragging = false;
        });
    });
  </script>
  
  <div class="graph-container">
    <svg id="graph"></svg>
  </div>
  
  <style>
    .graph-container {
      width: 100%;
      height: 100vh;  /* 화면 크기에 맞게 */
      padding: 20px;
      background-color: #f5f5f5;  /* 연한 회색 배경 */
      border-radius: 10px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 부드러운 그림자 */
      display: flex;
      justify-content: center;
      align-items: center;
      overflow: hidden;  /* 화면 밖으로 나가지 않도록 */
    }
  
    .node {
      fill: steelblue;
      stroke: white;
      stroke-width: 1.5px;
    }
  
    .link {
      stroke: #999;
      stroke-opacity: 0.6;
    }
  
    .node-label {
      font-size: 10px;
      fill: black;
      pointer-events: none;
    }
  
    svg {
      cursor: move; /* 드래그 가능 표시 */
    }
  </style>
  