<script>
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import { writable } from "svelte/store";
    
    // Store for dynamic graph data
    let graphData = writable({ nodes: [], links: [] });
    let userQuestion = ""; // For user input
    
    // Function to fetch data from backend
    async function fetchData() {
        try {
            console.log("그래프 뷰 요청...")
            const response = await fetch("/api/graphview/retrieve", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question: userQuestion }),
            });
            if (!response.ok) { // HTTP 응답 상태가 200이 아닌 경우
                throw new Error(`서버 오류: ${response.status}`);
            }

            const data = await response.json();  // JSON 파싱
            // graphData를 업데이트
            graphData.set(data);
            console.log(data);
            } catch (error) {
            console.error("데이터 요청 실패:", error);
         }
        
    }
    
    // Graph visualization logic
    onMount(() => {
        let svg, simulation;
        let width = window.innerWidth * 0.8; // 브라우저 너비의 80%
        let height = window.innerHeight * 0.8; // 브라우저 높이의 80%
    
        // Subscribe to changes in graphData
        graphData.subscribe(data => {
            d3.select("#graph").selectAll("*").remove(); // Clear existing SVG
    
            svg = d3.select("#graph")
                .attr("width", width)
                .attr("height", height);
    
            // Simulation setup
            simulation = d3.forceSimulation(data.nodes)
                .force("link", d3.forceLink(data.links).id(d => d.id).distance(150))
                .force("charge", d3.forceManyBody().strength(-300))
                .force("center", d3.forceCenter(width / 2, height / 2));
    
            // Draw links
            const link = svg.selectAll(".link")
                .data(data.links)
                .enter().append("line")
                .attr("class", "link")
                .attr("stroke", "#999")
                .attr("stroke-width", d => Math.sqrt(d.value));
    
            // Draw nodes
            const node = svg.selectAll(".node")
                .data(data.nodes)
                .enter().append("circle")
                .attr("class", "node")
                .attr("r", 10)
                .attr("fill", "skyblue")
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended));
    
            // Node labels
            svg.selectAll(".node-label")
                .data(data.nodes)
                .enter().append("text")
                .attr("class", "node-label")
                .text(d => d.label)
                .attr("x", 12)
                .attr("y", 3);
    
            // Simulation tick function
            simulation.on("tick", () => {
                link.attr("x1", d => d.source.x)
                    .attr("y1", d => d.source.y)
                    .attr("x2", d => d.target.x)
                    .attr("y2", d => d.target.y);
    
                node.attr("cx", d => d.x)
                    .attr("cy", d => d.y);
    
                svg.selectAll(".node-label")
                    .attr("x", d => d.x + 12)
                    .attr("y", d => d.y + 3);
            });
    
            // Drag functions
            function dragstarted(event) {
                if (!event.active) simulation.alphaTarget(0.3).restart();
                event.subject.fx = event.subject.x;
                event.subject.fy = event.subject.y;
            }
            function dragged(event) {
                event.subject.fx = event.x;
                event.subject.fy = event.y;
            }
            function dragended(event) {
                if (!event.active) simulation.alphaTarget(0);
                event.subject.fx = null;
                event.subject.fy = null;
            }
        });
    });
    </script>
    
    <div class="input-container">
        <input type="text" bind:value={userQuestion} placeholder="Enter your question..." />
        <button on:click={fetchData}>Submit</button>
    </div>
    
    <div class="graph-container">
        <svg id="graph"></svg>
    </div>
    
    <style>
    .graph-container {
        width: 100%;
        height: 100vh;
        background-color: #f5f5f5;
        border-radius: 10px;
    }
    .input-container {
        display: flex;
        justify-content: center;
        margin-bottom: 10px;
    }
    input {
        width: 300px;
        padding: 8px;
    }
    button {
        padding: 8px 16px;
        margin-left: 10px;
    }
    </style>
    