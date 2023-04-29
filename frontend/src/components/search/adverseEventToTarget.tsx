// Search by Adverse Event to Target
// Data of Interest: https://platform.opentargets.org/disease/MONDO_0005180 
import { TabPanel, Flex, Text, Center, Button } from '@chakra-ui/react'
import React, { useState } from 'react';
import { AsyncTypeahead } from 'react-bootstrap-typeahead';
import styles from "../../styles/Search.module.css"
import theme from '@/styles/theme';
import { useRouter } from 'next/router';

// Typeahead URI - DJANGO BACKEND
const SEARCH_URI =  process.env.NEXT_PUBLIC_HOST + '/api/suggest/adverse_event'
console.log(SEARCH_URI)

// Typeahead Async Search
function AdverseEventToTargetSearch() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [options, setOptions] = useState([]);
  const [selectedTypeAhead, setSelectedTypeAhead] = useState([]);

      const handleSearch = (query: string) => {
        setIsLoading(true);
        
        fetch(`${SEARCH_URI}/${query}`)
        .then((resp) => resp.json())
        .then((items) => {
          setOptions(items);
          setIsLoading(false);
        });
      };

      const handleChange = (selectedOptions) => {
        setSelectedTypeAhead(selectedOptions);
      };

       // @TODO Refactor this to be one reusable method
       const handleButtonClick = () => {
        router.push(`adverseEventToTarget/${selectedTypeAhead[0].meddraId}`)
      }

      const filterByCallback = (option, props) => {
        const query = props.text.toLowerCase();
        const adverseEventIdMatch = option.adverseEventId ? option.adverseEventId.toLowerCase().includes(query) : false;
        const meddraIdMatch = option.meddraId ? option.meddraId.toLowerCase().includes(query) : false;
        
        return adverseEventIdMatch || meddraIdMatch;
      };

      return (
        <TabPanel className={styles.searchInput}>
          <Text mb="4">Find targets that include this adverse event</Text>
        <AsyncTypeahead
          filterBy={filterByCallback}
          id="ae-to-target-search"
          isLoading={isLoading}
          labelKey="adverseEventId"
          minLength={1}
          onSearch={handleSearch}
          options={options}
          maxResults={25}
          placeholder="Search for an Adverse Event..."
          onChange={handleChange}
          inputProps={{ autoComplete: "off"}}
          renderMenuItemChildren={(ae) => (
            <>
              <Flex direction={"row"} className={styles.results}>
                <Text fontWeight="bold" className="adverse_event">
                  {ae["adverseEventId"]}
                </Text>

                <Text ml={"1"} className="id">
                  {ae["meddraId"]}
                </Text>
              </Flex>
            </>
          )}
        />
        <Center>
          <Button size="lg" bg={theme.brand.secondary} color="white" mt="5" onClick={handleButtonClick}>Search</Button>
        </Center>
        </TabPanel>
        
      );
    };

export default AdverseEventToTargetSearch;

