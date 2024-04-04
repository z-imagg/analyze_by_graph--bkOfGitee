// 节点
var nodes = new vis.DataSet([
  {id: 1, size: 29,label: "_1",shape: "dot",},
  { id: 20, label: "_20", color: "rgb(255,168,7)" },
  { id: 3, label: "_3", color: "#7BE141" },
  { id: 4, label: "_4", color: "rgba(97,195,238,0.5)" }, 
]);

// 边
var edges = new vis.DataSet([
  { from: 1, to: 3 },
  { from: 1, to: 20 },
  { from: 20, to: 4 }, 
]);

// 网络
var container = document.getElementById("mynetwork");
var data = {
  nodes: nodes,
  edges: edges,
};
// 可视化选项
var options = {
  nodes: { borderWidth: 2 },
  interaction: { hover: true },
  layout: { hierarchical: {  direction: "UD", 
  sortMethod: "directed",
},  },
edges: {
    arrows: "to",
  },
};
// 显示网络
var network = new vis.Network(container, data, options);
