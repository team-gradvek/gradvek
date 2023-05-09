import useSWR from 'swr'
import axios from 'axios'

function getPathwayData(path) {
  
  const fetcher = url => axios.get(url).then(res => res.data)

  const { data, isError, isLoading } = useSWR(`http://www.gradvek.org:8083/api/ae/path/${encodeURIComponent(path)}`, fetcher)

 
  return {
    data: data,
    isLoading: isLoading,
    isError: isError
  }
}

export default getPathwayData;
