// Search by Target to Adverse Event
// Data of Interest: https://platform.opentargets.org/target/ENSG00000151577
import { TabPanel, Flex, Text, Center, Button, Divider, Box } from '@chakra-ui/react'
import React, { useState } from 'react';
import { AsyncTypeahead } from 'react-bootstrap-typeahead';
import styles from "../../styles/Search.module.css"
import Link from 'next/link';
import theme from '@/styles/theme';
import { useRouter } from 'next/router';

// Typeahead URI - DJANGO BACKEND
const SEARCH_URI_TARGET =  process.env.NEXT_PUBLIC_HOST + '/api/suggest/target'
const SEARCH_URI_AE=  process.env.NEXT_PUBLIC_HOST + '/api/suggest/adverse_event'

// Typeahead Async Search
function DrugsByTargetAESearch() {
  const router = useRouter();


  const [isLoading, setIsLoading] = useState(false);
  

  const [optionsTarget, setOptionsTarget] = useState([]);
  const [optionsAE, setOptionsAE] = useState([]);

  const [selectedTypeAheadTarget, setSelectedTypeAheadTarget] = useState([]);
  const [selectedTypeAheadAE, setSelectedTypeAheadAE] = useState([]);

      const handleSearchTarget = (query) => {
        setIsLoading(true);
        
        fetch(`${SEARCH_URI_TARGET}/${query}`)
        .then((resp) => resp.json())
        .then((items) => {
          setOptionsTarget(items);
          setIsLoading(false);
        });
      };

      const handleSearchAE = (query) => {
        setIsLoading(true);

        fetch(`${SEARCH_URI_AE}/${query}`)
        .then((resp) => resp.json())
        .then((items) => {
          console.log(items)
          setOptionsAE(items);
          setIsLoading(false);
        });
      };

      const handleChangeTarget = (selectedOptionsTarget) => {
        setSelectedTypeAheadTarget(selectedOptionsTarget);
      };

      const handleChangeAE = (selectedOptionsAE) => {
        setSelectedTypeAheadAE(selectedOptionsAE);
      };

      

      // @TODO Refactor this to be one reusable method
      const handleButtonClick = () => {
        console.log("TARGET:")
        console.log(selectedTypeAheadTarget)
        console.log("AE:")
        console.log(selectedTypeAheadAE)
        router.push(`drugsByTargetAE/${selectedTypeAheadTarget[0].symbol}/${selectedTypeAheadAE[0].meddraId}`)
      }

      const filterByFieldsTarget = ['name', 'description'];
      const filterByFieldsAE = ['meddraId', 'adverseEventId'];
      
      return (
        <TabPanel className={styles.searchInput}>
          <Text mb="4">Search drugs associated with a target and adverse event</Text>

          <AsyncTypeahead
            filterBy={filterByFieldsTarget}
            id="target-search"
            isLoading={isLoading}
            labelKey="symbol"
            minLength={1}
            onSearch={handleSearchTarget}
            options={optionsTarget}
            maxResults={25}
            placeholder="Search for a Target..."
            onChange={handleChangeTarget}
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
        
         
         <Box mt={2}>
          <AsyncTypeahead
            filterBy={filterByFieldsAE}
            id="ae-search"
            isLoading={isLoading}
            labelKey="meddraId"
            minLength={1}
            onSearch={handleSearchAE}
            options={optionsAE}
            maxResults={25}
            placeholder="Search for a AE..."
            onChange={handleChangeAE}
            inputProps={{ autoComplete: "off", required: true}}
            renderMenuItemChildren={(ae) => (
              <>
                <Flex direction={"row"} className={styles.results}>
                  <Text fontWeight="bold" className="target-name">
                    {ae["meddraId"]}
                  </Text>
                  <Text ml={"1"} className="target-description">
                    {ae["adverseEventId"]}
                  </Text>
                </Flex>
              </>
            )}
          />
          </Box>
  
          <Center>
            <Button size="lg" bg={theme.brand.secondary} color="white" mt="5" onClick={handleButtonClick}>Search</Button>
          </Center>
        </TabPanel>
      );
    };
export default DrugsByTargetAESearch;
