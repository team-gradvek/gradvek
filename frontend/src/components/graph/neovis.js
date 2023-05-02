import NeoVis from 'neovis.js';
import neo4j from 'neo4j-driver';

const config = {
  container_id: 'viz',
  server_url: 'bolt://localhost:7687',
  server_user: 'neo4j',
  server_password: 'password',
  labels: {
    'Person': {
      caption: 'name',
      size: 'pagerank',
      community: 'community'
    }
  },
  relationships: {
    'ACTED_IN': {
      caption: false,
      thickness: 'weight'
    }
  }
};

const driver = neo4j.driver(
  config.server_url,
  neo4j.auth.basic(config.server_user, config.server_password)
);

const viz = new NeoVis(driver, config);
viz.render();
