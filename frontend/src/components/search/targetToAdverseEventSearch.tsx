// Search by Target to Adverse Event
// Data of Interest: https://platform.opentargets.org/target/ENSG00000151577
import { TabPanel, Flex, Text, Center, Button } from '@chakra-ui/react'
import React, { useState } from 'react';
import { AsyncTypeahead } from 'react-bootstrap-typeahead';
import styles from "../../styles/Search.module.css"
import theme from '@/styles/theme';
import { useRouter } from 'next/router';

// Typeahead URI - DJANGO BACKEND
const SEARCH_URI =  process.env.NEXT_PUBLIC_HOST + '/api/suggest/target'
console.log(SEARCH_URI)

// Typeahead Async Search
function TargetToAESearch() {
  const router = useRouter()
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

      const handleButtonClick = () => {
        router.push(`targetToAdverseEvents/${selectedTypeAhead[0].symbol}`)
      }

      const filterByFields = ['symbol'];

      return (
        <TabPanel className={styles.searchInput}>
          <Text mb="4">Find adverse events that include this target</Text>
        <AsyncTypeahead
          filterBy={filterByFields}
          id="target-to-ae-search"
          isLoading={isLoading}
          labelKey="symbol"
          minLength={1}
          onSearch={handleSearch}
          options={options}
          maxResults={25}
          placeholder="Search for a Target..."
          onChange={handleChange}
          inputProps={{ autoComplete: "off", required: true}}
          renderMenuItemChildren={(target) => (
            <>
              <Flex direction={"row"} className={styles.results}>
                <Text fontWeight="bold" className="target-name">
                  {target["symbol"]}
                </Text>
                <Text ml={"1"} className="target-description">
                  {target["name"]}
                </Text>
              </Flex>
            </>
          )}
        />
        <Center>
          <Button size="lg" bg={theme.brand.secondary} color="white" mt="5" onClick={handleButtonClick} id='submit'>Search</Button>
        </Center>
        </TabPanel>
      );
    };
export default TargetToAESearch;
