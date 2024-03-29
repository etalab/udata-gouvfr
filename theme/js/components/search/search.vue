<template>
  <div class="row-inline justify-between align-items-center search-bar">
    <search-input
      class="my-md my-md-xs fs-xl"
      :onChange="handleSearchChange"
      :value="queryString"
      :placeholder="$t('Search for data...')"
      ref="input"
    />
    <div
      class="filter-icon hidden visible-md w-auto mx-xs"
      :class="{ isFiltered, active: extendedForm }"
      v-html="filterIcon"
      @click="extendedForm = !extendedForm"
    ></div>
  </div>
  <div class="row-inline mt-sm justify-between align-items-center">
    <h1 class="m-0 h2">
      {{ $t("Datasets") }}<sup>{{ total_results || 0 }}</sup>
    </h1>
    <a :href="reuseUrl" title="" class="nav-link fs-sm mt-lg-sm hidden-md">
      {{ $t("Search reuses") }}
    </a>
  </div>
  <section class="search-filters p-md-md" :class="{ active: extendedForm }">
    <h4 class="mt-md mt-md-0 mb-xs mb-md-md fs-sm">
      {{ $t("Search filters") }}
    </h4>
    <div class="filters-wrapper p-sm p-md-0">
      <div class="row justify-between align-items-center">
        <div class="col-3 col-lg-6 col-md-12">
          <Suggestor
            :placeholder="$t('Organizations')"
            :searchPlaceholder="$t('Search an organization...')"
            listUrl="/organizations/?sort=-followers"
            suggestUrl="/organizations/suggest/"
            entityUrl="/organizations/"
            :values="facets.organization"
            :onChange="handleSuggestorChange('organization')"
          />
        </div>
        <div class="col-3 col-lg-6 col-md-12 mt-md-md">
          <Suggestor
            :placeholder="$t('Tags')"
            :searchPlaceholder="$t('Search a tag...')"
            suggestUrl="/tags/suggest/"
            :values="facets.tag"
            :onChange="handleSuggestorChange('tag')"
          />
        </div>
        <div class="col-3 col-lg-5 col-md-12 mt-lg-md">
          <Suggestor
            :placeholder="$t('Licenses')"
            :searchPlaceholder="$t('Search a license...')"
            listUrl="/datasets/licenses/"
            :values="facets.license"
            :onChange="handleSuggestorChange('license')"
          />
        </div>
        <div class="col-2 col-lg-5 col-md-12 mt-lg-md">
          <Suggestor
            :placeholder="$t('Formats')"
            :searchPlaceholder="$t('Search a format...')"
            suggestUrl="/datasets/suggest/formats/"
            :values="facets.format"
            :onChange="handleSuggestorChange('format')"
          />
        </div>
        <div
          class="col-1 col-lg-2 hidden-md text-align-center mt-lg-md text-align-right-lg"
        >
          <a
            class="btn-secondary btn-secondary-grey-200 px-md"
            @click="extendedForm = !extendedForm"
          >
            <span v-if="!extendedForm">…</span>
            <span v-else>X</span>
          </a>
        </div>
      </div>
      <div v-if="extendedForm" class="row mt-sm align-items-center">
        <div class="col-5 col-lg-6 col-md-12 row-inline">
          <Rangepicker
            :value="facets.temporal_coverage"
            :onChange="handleSuggestorChange('temporal_coverage')"
          />
        </div>
        <div class="col-3 col-md-12 mt-md-md">
          <Suggestor
            :placeholder="$t('Geographic area')"
            :searchPlaceholder="$t('Search a geographic area...')"
            suggestUrl="/spatial/zones/suggest/"
            entityUrl="/spatial/zone/"
            :values="facets.geozone"
            :onChange="handleSuggestorChange('geozone')"
          />
        </div>
        <div class="col-3 col-md-12 mt-md-md">
          <Suggestor
            :placeholder="$t('Territorial granularity')"
            :searchPlaceholder="$t('Search a granularity...')"
            listUrl="/spatial/granularities/"
            :values="facets.granularity"
            :onChange="handleSuggestorChange('granularity')"
          />
        </div>
      </div>
    </div>
    <div class="my-xl text-align-center hidden visible-md">
      <a
        class="btn-secondary btn-secondary-grey-400"
        @click="extendedForm = !extendedForm"
        >{{ $t("Submit") }}</a
      >
    </div>
  </section>
  <section class="search-results mt-lg mt-md-md">
    <transition mode="out-in">
      <div v-if="loading">
        <Loader />
      </div>
      <ul v-else-if="results.length">
        <a
          v-for="result in results"
          :key="result.id"
          :href="result.page"
          class="unstyled w-100"
        >
          <Dataset v-bind="result" />
        </a>
        <Pagination
          light
          v-if="total_results > page_size"
          :page="current_page"
          :page_size="page_size"
          :total_results="total_results"
          :changePage="changePage"
          class="mt-md"
        />
      </ul>
      <div v-else>
        <Empty
          wide
          :queryString="queryString"
          :cta="$t('Reset filters')"
          :copy="$t('No dataset matching your query')"
          :copyAfter="
            $t('You can try to reset the filters to expand your search.')
          "
          :onClick="() => resetFilters()"
        />
      </div>
    </transition>
  </section>
</template>

<script>
import config from "../../config";
import SearchInput from "./search-input";
import Suggestor from "./suggestor";
import Rangepicker from "./rangepicker";
import Dataset from "../dataset/search-result";
import Loader from "../dataset/loader";
import Empty from "./empty";
import Pagination from "../pagination/pagination";
import { generateCancelToken } from "../../plugins/api";
import filterIcon from "svg/filter.svg";

import queryString from "query-string";

export default {
  components: {
    "search-input": SearchInput,
    Rangepicker,
    Suggestor,
    Dataset,
    Empty,
    Loader,
    Pagination,
  },
  created() {
    this.filterIcon = filterIcon;

    //Update search params from URL on page load for deep linking
    const url = new URL(window.location);
    let searchParams = queryString.parse(url.search);
    if (searchParams.q) {
      this.queryString = searchParams.q;
      delete searchParams.q;
    }
    if (searchParams.page) {
      this.current_page = parseInt(searchParams.page);
      delete searchParams.page;
    }
    // set all other search params as facets
    this.facets = searchParams;
    this.search();
  },
  watch: {
    paramUrl: {
      deep: true,
      handler(val) {
        //Update URL to match current search params value for deep linking
        let url = new URL(window.location);
        const searchParams = queryString.stringify(val, { skipNull: true });
        url.search = searchParams;
        history.pushState(null, "", url);
      },
    },
  },
  data() {
    return {
      extendedForm: false, //On desktop, extended form is simply another row of filters. On mobile, form is hidden until extendedForm is triggered
      results: [],
      loading: false,
      currentRequest: null,
      page_size: 20,
      current_page: 1,
      total_results: 0,
      queryString: "",
      facets: {},
    };
  },
  computed: {
    //Url for doing the same search (queryString only) on the reuse page
    reuseUrl: function () {
      return `${config.values.reuseUrl}?q=${this.queryString}`;
    },
    //Is any filter active ?
    isFiltered: function () {
      return Object.keys(this.facets).some(
        (key) => this.facets[key]?.length > 0
      );
    },
    paramUrl: function() {
      let params = {};
      for (key in this.facets) {
        params[key] = this.facets[key];
      }
      if (this.current_page > 1)
        params.page = this.current_page;
      if (this.queryString)
        params.q = this.queryString;
      return params;
    }
  },
  methods: {
    handleSearchChange(input) {
      this.queryString = input;
      this.current_page = 1;
      this.search();
    },
    //Called on every facet selector change, updates the `facets.xxx` object then searches with new values
    handleSuggestorChange(facet) {
      return (values) => {
        //Values can either be an array of varying length, or a String.
        if (Array.isArray(values)) {
          if (values.length > 1)
            this.facets[facet] = values.map((obj) => obj.value);
          else if (values.length === 1) this.facets[facet] = values[0].value;
          else this.facets[facet] = null;
        } else {
          this.facets[facet] = values;
        }

        this.current_page = 1;
        this.search();
      };
    },
    changePage(page) {
      this.current_page = page;
      this.search();
      this.scrollToTop();
    },
    search() {
      this.loading = true;
      if (this.currentRequest) this.currentRequest.cancel();

      this.currentRequest = generateCancelToken();

      const promise = this.$api
        .get("/datasets/", {
          cancelToken: this.currentRequest.token,
          params: {
            q: this.queryString,
            ...this.facets,
            page_size: this.page_size,
            page: this.current_page,
          },
        })
        .then((res) => res.data)
        .then((result) => {
          this.results = result.data;
          this.total_results = result.total;
        })
        .finally(() => (this.loading = false));
    },
    scrollToTop() {
      if (this.$refs.input)
        this.$refs.input.$el.scrollIntoView({ behavior: "smooth" });
    },
    resetFilters() {
      this.queryString = "";
      this.facets = {};
      this.current_page = 1;
      this.search();
    },
  },
};
</script>
