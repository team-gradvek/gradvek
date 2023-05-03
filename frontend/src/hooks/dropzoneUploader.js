import { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Center, useColorModeValue, Icon, Box, Text } from '@chakra-ui/react';
import { AiFillFileAdd } from 'react-icons/ai';

function Uploader(props) {

  // const onDrop = useCallback((acceptedFiles) => {
  //   onFileAccepted(acceptedFiles[0]);
  // }, [onFileAccepted]);

  const { 
    getRootProps, 
    getInputProps,
    acceptedFiles, 
    // fileRejections, 
    isDragActive 
  } = useDropzone({
    // onDrop,
    // acceptedFiles,
    // fileRejections,
    accept: {
      'text/csv' : ['csv']
    }, 
    maxFiles: 1, 
    multiple: false,
  });

  const acceptedFileItems = acceptedFiles.map(file => (
     <Text>{file.path} - {file.size} bytes</Text> 
  ));

  // const fileRejectionItems = fileRejections.map(({ file, errors }) => (
  //   <li key={file.path}>
  //     {file.path} - {file.size} bytes
  //     <ul>
  //       {errors.map(e => (
  //         <li key={e.code}>{e.message}</li>
  //       ))}
  //     </ul>
  //   </li>
  // ));

  const dropText = isDragActive ? 'Drop the files here ...' : 'Drag \'n\' drop .csv file here, or click to select files';

  const activeBg = useColorModeValue('gray.100', 'gray.600');
  const borderColor = useColorModeValue(
    isDragActive ? 'teal.300' : 'gray.300',
    isDragActive ? 'teal.500' : 'gray.500',
  );

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
     
        <input {...getInputProps()} />
        <Icon as={AiFillFileAdd} mr={2}  />
        <Text>{dropText}</Text>
        {/* <h4>Rejected files</h4>
        <ul>{fileRejectionItems}</ul> */}
    </Center>
    <Center
      my={4}>
     {acceptedFileItems}
    </Center>
     </>
  );
}

export default Uploader