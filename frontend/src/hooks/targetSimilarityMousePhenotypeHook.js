import useSWR from 'swr'
import axios from 'axios'

function targetSimilarityMousePhenotype(id) {

  const fetcher = url => axios.get(url).then(res => res.data)

  const { data, error, isLoading } = useSWR(`http://localhost:8000/api/pheno/${encodeURIComponent(id)}`, fetcher)
  
  return {
    data: data,
    isLoading,
    isError: error
  }
}

export default targetSimilarityMousePhenotype;