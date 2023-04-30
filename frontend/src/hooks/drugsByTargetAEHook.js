import useSWR from 'swr'
import axios from 'axios'

function getDrugsByTargetAE(target, ae) {

  const fetcher = url => axios.get(url).then(res => res.data)

  const { data, error, isLoading } = useSWR(`http://localhost:8000/api/weight/${encodeURIComponent(target)}/${encodeURIComponent(ae)}`, fetcher)
 
  return {
    data: data,
    isLoading,
    isError: error
  }
}

export default getDrugsByTargetAE;