<template>
  <div class="avatar">
    <img :src="avatar_url" :alt="user.name + ' avatar'" />
  </div>
</template>

<script>
import config from "../../config";

export default {
  props: {
    user: Object,
  },
  computed: {
    avatar_url: function () {
      return this.user.avatar || this.identicon(this.user.id);
    },
  },
  methods: {
    identicon: function (id, size = 60) {
      return `${config.api_root}avatars/${id}/${size}`;
    },
  },
};
</script>
