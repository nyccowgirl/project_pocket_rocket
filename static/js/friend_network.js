/*jslint node: true */
'use strict';

$(document).ready(() => {

  $('#degree').on('submit', function(evt) {
    evt.preventDefault();
    let degreeInput = $("input[name='degree']:checked").val();
    let formInputs = {
      'degree': degreeInput
    };
    d3.json('/data.json?degree=' + degreeInput, makeForceGraph);

  });

  d3.json('/data.json', makeForceGraph);

  function makeForceGraph(error, data) {
    if (data.error === 'error') {
      return;
    }
    $('#network').html('');
    let dataNodes = data.nodes;
    let links = data.paths;
    let width = 1700;
    let height = 1000;

    let force = d3.forceSimulation(d3.values(dataNodes))
        .force('link', d3.forceLink(links).distance(60).strength(0.25))
        // .force("link", d3.forceLink().id(function(d) { return d.id; }).distance(60))
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


    let color = d3.scaleOrdinal(d3.schemeCategory20);
    // let color = d3.scaleOrdinal().range([rgb(123, 65, 115), rgb(165, 81, 148),
    //                                      rgb(140, 162, 82), rgb(206, 109, 189),
    //                                      rgb(222, 158, 214), rgb(82, 84, 163)
    //                                      rgb(173, 73, 74)]).range();

    node.append('circle')
        .attr('r', 7)
        .attr('fill', function(d) { return color(d.group); })
        // .style("fill", function(d) { return d.id; });
        .style('fill', function (d) {
          // console.log(d.source);
          // return color(d.group(getRandomInt(0, 19)));
          return color(d.group);
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

    function getRandomInt(min, max) {
      return Math.floor(Math.random() * (max - min + 1)) + min;
    }


  }

});