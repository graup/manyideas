import Vue from 'vue';
import Router from 'vue-router';
import Start from '@/components/pages/Start';
import Login from '@/components/pages/Login';
import Signup from '@/components/pages/Signup';
import SignupConsent from '@/components/pages/SignupConsent';
import SignupTest from '@/components/pages/SignupTest';
import Feed from '@/components/pages/Feed';
import MyFeed from '@/components/pages/MyFeed';
import MyReactionFeed from '@/components/pages/MyReactionFeed';
import IssueDetails from '@/components/pages/IssueDetails';
import NewIssue from '@/components/pages/NewIssue';
import FAQ from '@/components/pages/FAQ';

Vue.use(Router);

export default new Router({
  mode: 'history',
  scrollBehavior(to, from, savedPosition) {
    return new Promise((resolve) => {
      setTimeout(() => {
        if (savedPosition) {
          resolve(savedPosition);
        }
        resolve({ x: 0, y: 0 });
      }, 550);
    });
  },
  routes: [
    { path: '/', name: 'start', component: Start },
    { path: '/login', name: 'login', component: Login, meta: { unauth: true } },
    { path: '/signup', name: 'signup', component: Signup, meta: { unauth: true } },
    { path: '/signup-consent', name: 'signup-consent', component: SignupConsent, meta: { unauth: true } },
    { path: '/signup-test', name: 'signup-test', component: SignupTest, meta: { auth: true } },
    { path: '/feed', name: 'feed', component: Feed, meta: { auth: true } },
    { path: '/faq', name: 'faq', component: FAQ, meta: { auth: true } },
    { path: '/my-posts', name: 'my-posts', component: MyFeed, meta: { auth: true } },
    { path: '/my-reactions', name: 'my-reactions', component: MyReactionFeed, meta: { auth: true } },
    { path: '/issues/new', name: 'new-issue', component: NewIssue, meta: { auth: true } },
    {
      path: '/issues/:slug',
      name: 'issue-detail',
      component: IssueDetails,
      props: true,
    },
  ],
});
