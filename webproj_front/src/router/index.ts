import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/Home.vue')
    },
    // Dialog routes
    {
      path: '/dialogs',
      name: 'dialogs',
      component: () => import('../components/dialogs/OpenerList.vue')
    },
    // Profile routes
    {
      path: '/profiles',
      name: 'profiles',
      component: () => import('../components/profiles/ProfileList.vue')
    },
    {
      path: '/profiles/:id',
      name: 'profile-details',
      component: () => import('../components/profiles/ProfileDetails.vue')
    },
    // Story routes
    {
      path: '/stories',
      name: 'stories',
      component: () => import('../components/stories/StoryList.vue')
    },
    {
      path: '/stories/:id',
      name: 'story-details',
      component: () => import('../components/stories/StoryDetails.vue')
    },
    // Error routes
    {
      path: '/404',
      name: 'not-found',
      component: () => import('../views/NotFound.vue')
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/404'
    }
  ]
})

// Comment out or remove the authentication guard for now
// router.beforeEach((to, from, next) => {
//   const publicPages = ['/login', '/register', '/404']
//   const authRequired = !publicPages.includes(to.path)
//   const loggedIn = localStorage.getItem('token')

//   if (authRequired && !loggedIn) {
//     return next('/login')
//   }

//   next()
// })

export default router
