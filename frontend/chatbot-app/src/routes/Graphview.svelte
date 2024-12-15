<script>
    import { onMount } from "svelte";
    import * as d3 from "d3";
    import { writable } from "svelte/store";

    let graphData = writable({ nodes: [], links: [] });
    let userQuestion = ""; // For user input
    let loading = false;
    let loadingTime = 0;
    let timer;
    
    // 상태 창 데이터와 가시성 관리
    let selectedNode = null;
    let isPanelOpen = false;

    async function fetchData() {
        try {
            loading = true;
            timer = setInterval(() => {
                loadingTime++;
            }, 1000);
            const response = await fetch("/api/graphview/retrieve", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question: userQuestion }),
            });
            if (!response.ok) throw new Error(`서버 오류: ${response.status}`);
            const data = await response.json();
            graphData.set(data);
        } catch (error) {
            console.error("데이터 요청 실패:", error);
        } finally {
            loading = false;
            clearInterval(timer);
        }
    }
    function handleNodeClick1(event, d) {
    // 노드의 정보를 콘솔에 출력
    console.log('클릭된 노드 정보:', d);
    // 예시: 클릭된 노드의 id와 label을 출력
    console.log('Node ID:', d.id);
    console.log('Node Label:', d.label);
}

    async function handleNodeClick(event, d) {
        selectedNode = d; // 클릭된 노드의 정보를 저장
        isPanelOpen = true; // 패널을 열기

        // 상태 변경 후 화면을 강제로 렌더링하도록 tick 호출
        await tick();
    }

    function closePanel() {
        isPanelOpen = false;
    }

    onMount(() => {
        let svg, simulation;
        let width = window.innerWidth * 0.8;
        let height = window.innerHeight * 0.8;

        graphData.subscribe(data => {
            d3.select("#graph").selectAll("*").remove();

            svg = d3.select("#graph")
                .attr("width", width)
                .attr("height", height);

            simulation = d3.forceSimulation(data.nodes)
                .force("link", d3.forceLink(data.links).id(d => d.id).distance(150))
                .force("charge", d3.forceManyBody().strength(-300))
                .force("center", d3.forceCenter(width / 2, height / 2));

            const link = svg.selectAll(".link")
                .data(data.links)
                .enter().append("line")
                .attr("class", "link")
                .attr("stroke", "#999")
                .attr("stroke-width", d => Math.max(Math.sqrt(d.value), 0.2));

            const node = svg.selectAll(".node")
                .data(data.nodes)
                .enter().append("circle")
                .attr("class", "node")
                .attr("r", 10)
                .attr("fill", "skyblue")
                .on("click", handleNodeClick) // 노드 클릭 이벤트
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended));

            svg.selectAll(".node-label")
                .data(data.nodes)
                .enter().append("text")
                .attr("class", "node-label")
                .text(d => d.id)
                .attr("x", 12)
                .attr("y", 3);

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

{#if loading}
<div class="loading-message">그래프뷰 생성중... {loadingTime}</div>
{/if}

<div class="graph-container">
    <svg id="graph"></svg>
</div>

<div class="info-panel {isPanelOpen ? 'open' : ''}">
    {#if selectedNode}
    <div class="panel-content">
        <h3>Node Information</h3>
        <p><strong>ID:</strong> {selectedNode.id}</p>
        <p><strong>Label:</strong> {selectedNode.label}</p>
        <button on:click={closePanel}>Close</button>
    </div>
    {/if}
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
.info-panel {
    position: fixed;
    top: 0;
    right: -300px;
    width: 300px;
    height: 100%;
    background-color: white;
    box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1);
    transition: right 0.3s ease;
    padding: 20px;
}
.info-panel.open {
    right: 0;
}
.panel-content h3 {
    margin-top: 0;
}
.panel-content button {
    margin-top: 10px;
}
</style>
