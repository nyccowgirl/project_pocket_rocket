/*jslint node: true */
'use strict';

$(document).ready(() => {
  d3.json('/data.json', makeForceGraph);

  function makeForceGraph(error, data) {
    let dataNodes = data.nodes;
    let links = data.paths;
    let width = 1700;
    let height = 1000;

    let force = d3.forceSimulation(d3.values(dataNodes))
        .force('link', d3.forceLink(links).distance(60).strength(0.25))
        .force('center', d3.forceCenter(width / 2, height/ 2))
        .force('charge', d3.forceManyBody())
        .on('tick', tick);

    let svg = d3.select('#network')
        .append('svg')
        .attr('width', width)
        .attr('height', height);

    // add the links and the arrows

    let link = svg.selectAll('.link')
        .data(links)
        .enter()
          .append('line')
          .attr('class', 'link');

    // define the nodes

    let node = svg.selectAll('.node')
        .data(force.nodes())
        .enter()
          .append('g')
          .attr('class', 'node')
          .call(d3.drag()
              .on('start', dragstarted)
              .on('drag', dragged)
              .on('end', dragended));

    let color = d3.scaleOrdinal(d3.schemeCategory10);

    node.append('circle')
        .attr('r', 7)
        .style('fill', function (d) {
          console.log(d.source);
          return color(d.adviser);
        });

    // add the text

    node.append('text')
        .attr('x', 6)
        .text(function (d) {
          return d.name;
        });

    // "schproing!"

    function tick() {
      link.attr('x1', function (d) {
            return d.source.x;
          })
          .attr('y1', function (d) {
            return d.source.y;
          })
          .attr('x2', function (d) {
            return d.target.x;
          })
          .attr('y2', function (d) {
            return d.target.y;
          });

      node.attr('transform', function (d) {
        return 'translate(' + d.x + ',' + d.y + ')';
      });
    }

    function dragstarted(d) {
      if (!d3.event.active) {
        force.alphaTarget(0.3).restart();
      }
    }

    function dragged(d) {
      d.fx = d3.event.x;
      d.fy = d3.event.y;
    }

    function dragended(d) {
      if (!d3.event.active) {
        force.alphaTarget(0);
      }

      d.fx = null;
      d.fy = null;
    }



  }
});