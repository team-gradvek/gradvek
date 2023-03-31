function Home({descriptors}) {
  return (
      <>
      <div>
          console.log(descriptors)
          {descriptors.map((descriptor) => (
              <p>{descriptor.descriptor_name}</p>
          ))}
      </div>
      </>
  )
}



export async function getStaticProps() {
  const res = await fetch("http://localhost:8000/api/descriptors")
  const descriptors = await res.json();

  return{
      props: {
          descriptors
      }
  }
}


export default Home