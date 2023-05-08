import { useCallback, useState, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import { Center, useColorModeValue, Icon, Box, Text, Button, Progress } from '@chakra-ui/react';
import { AiFillFileAdd} from 'react-icons/ai';
import { BsFiletypeCsv } from "react-icons/bs";
import axios from 'axios';

function Uploader(props) {

  // Set state for files
  const [files, setFiles] = useState([])

  // Set state of the upload
  const [fileSent, setFileSent] = useState([])

  const { 
    getRootProps, 
    getInputProps,
    acceptedFiles, 
    // fileRejections, 
    isDragActive 
  } = useDropzone({
    accept: {
      'text/csv' : ['csv']
    }, 
    maxFiles: 1, 
    multiple: false,
    onDrop: acceptedFiles => {
      setFiles(acceptedFiles)
    }
  });

  // GOutput the file name and csv icon
  const thumbs = files.map(file => (
    <div key={file.name}>
      <Text><Icon as={BsFiletypeCsv}/> {file.name} - {file.size} KB</Text>
    </div>
  ))


  const dropText = isDragActive ? 'Drop the files here ...' : 'Drag \'n\' drop .csv file here, or click to select files';

  const activeBg = useColorModeValue('gray.100', 'gray.600');
  const borderColor = useColorModeValue(
    isDragActive ? 'teal.300' : 'gray.300',
    isDragActive ? 'teal.500' : 'gray.500',
  );

  const [loading, setLoading] = useState(false)

  const uploadFile = () => {
    if(acceptedFiles[0] != null) {
      setLoading(true)
      const formData = new FormData()
      console.log(files)
      formData.append('csv_file', acceptedFiles[0])
      // console.log(formData)
      axios.post('http://localhost:8000/api/csv/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }, 
      // onUploadProgress,
    }).then(function(response){
      setLoading(false)
      setFiles([])
    })
      .catch(() => {
        //if error, display a message
        console.log("error uploading file")
        setLoading(false)
      })
    }
  }

  const handleFile = (e) => {
    setFileSent(e.target.files[0])
    console.log(fileSent)
  }

  return (
    <>
    <Center
      p={10}
      cursor="pointer"
      bg={isDragActive ? activeBg : 'transparent'}
      _hover={{ bg: activeBg }}
      transition="background-color 0.2s ease"
      borderRadius={4}
      border="3px dashed"
      borderColor={borderColor}
      {...getRootProps({className: 'dropzone'})}
    >
     
        <input {...getInputProps({
          onChange: handleFile,
        })} name='csv_file' type='file' id='csv_file'/>
        <Icon as={AiFillFileAdd} mr={2}  />
        <Text>{dropText}</Text>
    </Center>
    <Center mt={4}>{thumbs}</Center>
    {loading && <Progress size="xs" isIndeterminate />}
    {loading && <Center my={2}> Processing File</Center>}
    <Center mt={4}><Button colorScheme='blue' onClick={() => uploadFile()}>Upload File</Button></Center>
     </>
  );
}

export default Uploader