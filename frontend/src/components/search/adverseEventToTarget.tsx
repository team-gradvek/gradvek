// Search by Adverse Event to Target
import { TabPanel, Flex, Text } from '@chakra-ui/react'
import React, { useState } from 'react';
import { AsyncTypeahead } from 'react-bootstrap-typeahead';
import styles from "../../styles/Search.module.css"

// Typeahead URI - DJANGO BACKEND
const SEARCH_URI = 'http://localhost:8000/api/adverse-events'

// Typeahead Async Search
function AdverseEventToTargetSearch() {
  const [isLoading, setIsLoading] = useState(false);
  const [options, setOptions] = useState([]);
  const [selectedTypeAhead, setSelectedTypeAhead] = useState([]);

      const handleSearch = (query: string) => {
        setIsLoading(true);
        
        fetch(`${SEARCH_URI}`)
        .then((resp) => resp.json())
        .then((items) => {
          setOptions(items);
          setIsLoading(false);
        });
      };

      const handleChange = (selectedOptions) => {
        setSelectedTypeAhead(selectedOptions);
      };

      const filterByFields = ['name', 'description'];


      return (
        <TabPanel className={styles.searchInput}>
          <Text mb="4">Find targets that include this adverse event</Text>
        <AsyncTypeahead
          filterBy={filterByFields}
          id="ae-to-target-search"
          isLoading={isLoading}
          labelKey="name"
          minLength={2}
          onSearch={handleSearch}
          options={options}
          maxResults={25}
          placeholder="Search for an Adverse Event..."
          onChange={handleChange}
          inputProps={{ autoComplete: "off"}}
          renderMenuItemChildren={(ae) => (
            <>
              <Flex direction={"row"} className={styles.results}>
                <Text fontWeight="bold" className="name">
                  {ae["name"]}
                </Text>

                <Text ml={"1"} className="description">
                  {ae["description"]}
                </Text>
              </Flex>
            </>
          )}
        />
        </TabPanel>
      );
    };

export default AdverseEventToTargetSearch;

