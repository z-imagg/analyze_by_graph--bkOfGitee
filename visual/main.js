//节点
var default_nodeLs=[
  {id: 1, xxx:444,size: 29,label: "_1",shape: "square", },
  { id: 20,size: 20, label: "_20",shape: "dot", color: "rgb(255,168,7)" },
  { id: 3, label: "_3", color: "#7BE141" },
  { id: 4, label: "_4", color: "rgba(97,195,238,0.5)" }, 
];
var existed_generated_nodeLs_visjs= (typeof generated_nodeLs_visjs != 'undefined');
var nodeLs=existed_generated_nodeLs_visjs?generated_nodeLs_visjs:default_nodeLs;
var nodes = new vis.DataSet(nodeLs);

//边
var default_edgeLs=[
  { from: 1, to: 3 },
  { from: 1, to: 20 },
  { from: 20, to: 4 }, 
];
var existed_generated_edgeLs_visjs= (typeof generated_edgeLs_visjs != 'undefined');
var edgeLs=existed_generated_edgeLs_visjs?generated_edgeLs_visjs:default_edgeLs;
var edges = new vis.DataSet(edgeLs);

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
