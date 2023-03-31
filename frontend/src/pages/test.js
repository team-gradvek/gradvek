function Home({descriptors}) {
  return (
      <>
          {descriptors.map((descriptor) => (
              <p key={descriptor.descriptor_name}>{descriptor.descriptor_name}</p>
          ))}
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