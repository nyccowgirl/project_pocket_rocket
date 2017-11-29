/*jslint node: true */
'use strict';

$(document).ready(() => {

  $(function(){
    $('#chart').dxChart({
      dataSource: dataSource,
      commonSeriesSettings: {
          type: 'bubble'
      },
      title: 'Correlation between Total Check-Ins and Total Referrals',
      tooltip: {
          enabled: true,
          location: 'edge',
          customizeTooltip: function (arg) {
              return {
                  text: arg.point.tag + '<br/>Total Check-Ins: ' + arg.argumentText + '<br/>Total Referrals: ' + arg.valueText + '<br/>Total Redemptions: ' + arg.size
              };
          }
      },
      argumentAxis: {
          label: {
              customizeText: function () {
                  return this.value;
              }
          },
          title: 'Total Check-Ins'
      },
      valueAxis: {
          label: {
              customizeText: function () {
                  return this.value;
              }
          },
          title: 'Total Referrals'
      },
      legend: {
          position: 'outside',
          verticalAlignment: 'top',
          horizontalAlignment: 'center',
          border: {
              visible: true
          }
      },
      palette: ['#586f75', '#aedce7', '#2d2f35', '#cc6649', '#468499', '#b72b3d', '#bd6578', '#bcdbdb', '#4a9590', '#8d5176', '#b482aa', '#e3c0dc', '#fdd1e3'],
      onSeriesClick: function(e) {
          var series = e.target;
          if (series.isVisible()) {
              series.hide();
          } else {
              series.show();
          }
      },
      'export': {
          enabled: true
      },
      series: [{
          name: 'Bar',
          argumentField: 'total1',
          valueField: 'older1',
          sizeField: 'perc1',
          tagField:'tag1'
      }, {
          name: 'Cleaners',
          argumentField: 'total2',
          valueField: 'older2',
          sizeField: 'perc2',
          tagField: 'tag2'
      }, {
          name: 'Coffee/Cafe/Tea',
          argumentField: 'total3',
          valueField: 'older3',
          sizeField: 'perc3',
          tagField: 'tag3'
      }, {
          name: 'Deli/Grocery',
          argumentField: 'total4',
          valueField: 'older4',
          sizeField: 'perc4',
          tagField: 'tag4'
      }, {
          name: 'Florist',
          argumentField: 'total5',
          valueField: 'older5',
          sizeField: 'perc5',
          tagField: 'tag5'
      }, {
          name: 'Home Services',
          argumentField: 'total6',
          valueField: 'older6',
          sizeField: 'perc6',
          tagField: 'tag6'
      }, {
          name: 'Medical Services',
          argumentField: 'total7',
          valueField: 'older7',
          sizeField: 'perc7',
          tagField: 'tag7'
      }, {
          name: 'Legal Services',
          argumentField: 'total8',
          valueField: 'older8',
          sizeField: 'perc8',
          tagField: 'tag8'
      }, {
          name: 'Nightlife',
          argumentField: 'total9',
          valueField: 'older9',
          sizeField: 'perc9',
          tagField: 'tag9'
      }, {
          name: 'Pets',
          argumentField: 'total10',
          valueField: 'older10',
          sizeField: 'perc10',
          tagField: 'tag10'
      }, {
          name: 'Restaurant',
          argumentField: 'total11',
          valueField: 'older11',
          sizeField: 'perc11',
          tagField: 'tag11'
      }, {
          name: 'Salon',
          argumentField: 'total12',
          valueField: 'older12',
          sizeField: 'perc12',
          tagField: 'tag12'
      }, {
          name: 'Spa',
          argumentField: 'total13',
          valueField: 'older13',
          sizeField: 'perc13',
          tagField: 'tag13'
      }]
    });
  });
});
