import useSWR from 'swr'
import axios from 'axios'

function getTargetData(id) {

  const fetcher = url => axios.get(url).then(res => res.data)

  const { data, error, isLoading } = useSWR(`http://www.gradvek.org:8083/api/ae-weight/${encodeURIComponent(id)}`, fetcher)
  
  return {
    data: data,
    isLoading,
    isError: error
  }
}

export default getTargetData;
