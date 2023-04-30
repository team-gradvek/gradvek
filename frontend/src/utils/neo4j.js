import { driver, auth } from 'neo4j-driver';

const neo4jUri = process.env.NEO4J_URI || 'bolt://localhost:7687';
const neo4jUser = process.env.NEO4J_USER || 'neo4j';
const neo4jPassword = process.env.NEO4J_PASSWORD || 'gradvek1';

const neo4jDriver = driver(neo4jUri, auth.basic(neo4jUser, neo4jPassword));

console.log(neo4jDriver)

export default neo4jDriver;
