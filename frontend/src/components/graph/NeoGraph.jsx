import React, { useEffect } from 'react';
import NeoVis from 'neovis.js'


// this file is to be deleted - @ALI this is for you to see how i got the connection working
const Neo4jVisualization = () => {
  useEffect(() => {
    const config = {
      container_id: 'viz',
      server_url: 'bolt://neo4j:7687',
      server_user: 'neo4j',
      server_password: 'gradvek1',
      labels: {
        'AdverseEvent': {
          caption: 'name',
          size: 'pagerank',
          community: 'community'
        }
      },
    };

    const driver = neo4j.driver(
      config.server_url,
      neo4j.auth.basic(config.server_user, config.server_password)
    );

    const viz = new NeoVis(driver, config);
    viz.render();
  }, []);

  return <div id="viz"></div>;
};

export default Neo4jVisualization;
